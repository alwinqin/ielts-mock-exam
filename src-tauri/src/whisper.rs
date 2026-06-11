use tauri::{AppHandle, Manager};
use std::io::Write;
use std::process::Command;
use std::path::PathBuf;

fn get_whisper_binary(app: &AppHandle) -> Result<PathBuf, String> {
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let bin = if cfg!(target_os = "windows") {
        resource_dir.join("binaries/whisper-cli.exe")
    } else {
        resource_dir.join("binaries/whisper-cli")
    };
    if bin.exists() {
        return Ok(bin);
    }
    let name = if cfg!(target_os = "windows") { "whisper-cli.exe" } else { "whisper-cli" };
    for dir in std::env::split_paths(&std::env::var("PATH").unwrap_or_default()) {
        let c = dir.join(name);
        if c.exists() {
            return Ok(c);
        }
    }
    Err("whisper-cli binary not found".to_string())
}

fn get_model_path(app: &AppHandle) -> Result<PathBuf, String> {
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let model = data_dir.join("models/ggml-tiny.en.bin");
    if model.exists() {
        return Ok(model);
    }
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let alt = resource_dir.join("binaries/ggml-tiny.en.bin");
    if alt.exists() {
        return Ok(alt);
    }
    Err(format!("Model not found. Download ggml-tiny.en.bin to '{}'", data_dir.join("models").display()))
}

/// Convert audio to 16kHz mono WAV via ffmpeg so whisper-cli can decode it.
/// Falls back to original file if ffmpeg is unavailable or conversion fails.
fn normalize_audio(input: &PathBuf, output: &PathBuf) -> Result<(), String> {
    let result = Command::new("ffmpeg")
        .arg("-y")
        .arg("-i").arg(input)
        .arg("-ar").arg("16000")
        .arg("-ac").arg("1")
        .arg("-sample_fmt").arg("s16")
        .arg("-f").arg("wav")
        .arg(output)
        .output()
        .map_err(|e| format!("ffmpeg not found: {}", e))?;
    if !result.status.success() {
        let stderr = String::from_utf8_lossy(&result.stderr);
        return Err(format!("ffmpeg conversion failed: {}", stderr));
    }
    Ok(())
}

#[tauri::command]
pub async fn transcribe(audio: Vec<u8>, app: AppHandle) -> Result<String, String> {
    let whisper_bin = get_whisper_binary(&app)?;
    let model_path = get_model_path(&app)?;

    let suffix: u32 = {
        use std::time::{SystemTime, UNIX_EPOCH};
        let dur = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default();
        (dur.as_nanos() % 1_000_000) as u32
    };
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let temp_input = data_dir.join(format!("_audio_in_{}.wav", suffix));
    let temp_wav = data_dir.join(format!("_audio_16k_{}.wav", suffix));
    let txt_path = data_dir.join(format!("_transcript_{}.txt", suffix));

    // RAII cleanup
    struct Cleanup { files: Vec<PathBuf> }
    impl Drop for Cleanup {
        fn drop(&mut self) {
            for f in &self.files { std::fs::remove_file(f).ok(); }
        }
    }
    let _guard = Cleanup { files: vec![temp_input.clone(), temp_wav.clone(), txt_path.clone()] };

    // Write raw audio bytes to temp file
    {
        let mut f = std::fs::File::create(&temp_input).map_err(|e| e.to_string())?;
        f.write_all(&audio).map_err(|e| e.to_string())?;
    }

    // Convert to 16kHz mono WAV (whisper-cli only reliably decodes WAV/PCM)
    let audio_for_whisper = match normalize_audio(&temp_input, &temp_wav) {
        Ok(()) => temp_wav.clone(),
        Err(_) => temp_input.clone(), // fallback: try raw input
    };

    let output = Command::new(&whisper_bin)
        .arg("-m").arg(model_path.to_str().ok_or("Invalid model path")?)
        .arg("-f").arg(audio_for_whisper.to_str().ok_or("Invalid audio path")?)
        .arg("--language").arg("en")
        .arg("-otxt")
        .arg("-of").arg(data_dir.join(format!("_transcript_{}", suffix)).to_str().ok_or("Invalid output")?)
        .output()
        .map_err(|e| format!("whisper-cli failed: {}", e))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("whisper-cli error: {}", stderr));
    }

    let text = std::fs::read_to_string(&txt_path)
        .map_err(|e| format!("Failed to read transcript: {}", e))?;

    Ok(text.trim().to_string())
}
