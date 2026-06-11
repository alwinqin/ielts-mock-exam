fn main() {
    // Track www/ frontend changes so generate_context!() re-embeds updated files
    println!("cargo:rerun-if-changed=../www");
    tauri_build::build()
}
