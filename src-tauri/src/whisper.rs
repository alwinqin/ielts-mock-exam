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
    let paths = std::env::var("PATH").unwrap_or_default();
    let exe_name = if cfg!(target_os = "windows") { "whisper-cli.exe" } else { "whisper-cli" };
    for dir in paths.split(':') {
        let candidate = PathBuf::from(dir).join(exe_name);
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

    // Write audio to a temp file
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let temp_audio = data_dir.join("_temp_audio.wav");
    {
        let mut f = std::fs::File::create(&temp_audio).map_err(|e| e.to_string())?;
        f.write_all(&audio).map_err(|e| e.to_string())?;
    }

    // Run whisper-cli
    let output = Command::new(&whisper_bin)
        .arg("-m")
        .arg(model_path.to_str().unwrap_or("ggml-tiny.en.bin"))
        .arg("-f")
        .arg(temp_audio.to_str().unwrap_or("_temp_audio.wav"))
        .arg("--language")
        .arg("en")
        .arg("--output-txt")
        .arg("--output-file")
        .arg(data_dir.join("_temp_transcript").to_str().unwrap_or("_temp_transcript"))
        .output()
        .map_err(|e| format!("Failed to run whisper-cli: {}", e))?;

    // Clean up temp audio
    std::fs::remove_file(&temp_audio).ok();

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("whisper-cli error: {}", stderr));
    }

    // Read the output text file
    let txt_path = data_dir.join("_temp_transcript.txt");
    let text = std::fs::read_to_string(&txt_path)
        .map_err(|e| format!("Failed to read transcript: {}", e))?;
    std::fs::remove_file(&txt_path).ok();

    Ok(text.trim().to_string())
}
