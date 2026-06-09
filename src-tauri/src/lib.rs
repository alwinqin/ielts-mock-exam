use tauri::Manager;

mod whisper;

#[tauri::command]
async fn get_audio_path(test_id: String, _section_idx: usize, app: tauri::AppHandle) -> Result<String, String> {
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let audio_dir = if test_id.starts_with("cam") {
        resource_dir.join("data/cambridge/audio")
    } else {
        resource_dir.join("data/listening/audio")
    };
    Ok(audio_dir.to_string_lossy().to_string())
}

#[tauri::command]
async fn get_app_data_dir(app: tauri::AppHandle) -> Result<String, String> {
    let data_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    Ok(data_dir.to_string_lossy().to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            get_audio_path,
            get_app_data_dir,
            whisper::transcribe,
        ])
        .setup(|app| {
            // Ensure data directories exist
            let data_dir = app.path().app_data_dir()?;
            std::fs::create_dir_all(&data_dir).ok();
            let models_dir = data_dir.join("models");
            std::fs::create_dir_all(&models_dir).ok();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
