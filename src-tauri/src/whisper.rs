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
    // Fallback: try PATH lookup
    let exe_name = if cfg!(target_os = "windows") { "whisper-cli.exe" } else { "whisper-cli" };
    for dir in std::env::split_paths(&std::env::var("PATH").unwrap_or_default()) {
        let candidate = dir.join(exe_name);
        if candidate.exists() {
            return Ok(candidate);
        }
    }
    Err("whisper-cli binary not found. Please install whisper.cpp.".to_string())
}

fn get_model_path(app: &AppHandle) -> Result<PathBuf, String> {
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let models_dir = data_dir.join("models");
    let model = models_dir.join("ggml-tiny.en.bin");
    if model.exists() {
        return Ok(model);
    }
    // Check resource directory
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let model_alt = resource_dir.join("binaries/ggml-tiny.en.bin");
    if model_alt.exists() {
        return Ok(model_alt);
    }
    Err(format!(
        "Model not found. Download ggml-tiny.en.bin to '{}'",
        models_dir.display()
    ))
}

#[tauri::command]
pub async fn transcribe(audio: Vec<u8>, app: AppHandle) -> Result<String, String> {
    let whisper_bin = get_whisper_binary(&app)?;
    let model_path = get_model_path(&app)?;

    // Use random suffix to prevent concurrent call collisions (fixed temp file names)
    let suffix: u32 = {
        use std::time::{SystemTime, UNIX_EPOCH};
        let dur = SystemTime::now().duration_since(UNIX_EPOCH).unwrap_or_default();
        (dur.as_nanos() % 1_000_000) as u32
    };
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let temp_audio = data_dir.join(format!("_temp_audio_{}.wav", suffix));
    let txt_path = data_dir.join(format!("_temp_transcript_{}.txt", suffix));

    // RAII-style cleanup: remove temp files on scope exit
    struct TempGuard { audio: PathBuf, txt: PathBuf }
    impl Drop for TempGuard {
        fn drop(&mut self) {
            std::fs::remove_file(&self.audio).ok();
            std::fs::remove_file(&self.txt).ok();
        }
    }
    let _guard = TempGuard { audio: temp_audio.clone(), txt: txt_path.clone() };

    // Write audio to temp file
    {
        let mut f = std::fs::File::create(&temp_audio).map_err(|e| e.to_string())?;
        f.write_all(&audio).map_err(|e| e.to_string())?;
    }

    // Run whisper-cli
    let output = Command::new(&whisper_bin)
        .arg("-m")
        .arg(model_path.to_str().ok_or("Invalid model path (non-UTF8)")?)
        .arg("-f")
        .arg(temp_audio.to_str().ok_or("Invalid audio path (non-UTF8)")?)
        .arg("--language")
        .arg("en")
        .arg("--output-txt")
        .arg("--output-file")
        .arg(data_dir.join(format!("_temp_transcript_{}", suffix)).to_str().ok_or("Invalid output path (non-UTF8)")?)
        .output()
        .map_err(|e| format!("Failed to run whisper-cli: {}", e))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("whisper-cli error: {}", stderr));
    }

    // Read the output text file
    let text = std::fs::read_to_string(&txt_path)
        .map_err(|e| format!("Failed to read transcript: {}", e))?;

    Ok(text.trim().to_string())
}
