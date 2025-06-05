# SAI3_Chatbot
Group E

C++ wird benötigt als Code interpreter

---

## For Mac

### Prerequisites

1. **Download the LLM model file**  
   - Download `llama-2-7b-chat.Q4_K_M.gguf` from:  
     https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf  
   - Place the downloaded file into the `models/` directory of this project.

2. **Activate your Python virtual environment**  
   - If you haven’t created one yet:
     ```bash
     python3 -m venv .venv
     ```
   - Then activate it:
     ```bash
     source .venv/bin/activate
     ```
     
---

### Installation (macOS)

On macOS, a full C++ toolchain with standard‐library headers is required. You must install Xcode (or at least the Xcode SDK) before proceeding:

1. **Install Xcode from the App Store**  
   - Open the App Store, search for “Xcode,” and click **Get** (or “Update” if it’s already installed).  
   - Once it’s finished downloading, launch Xcode at least once and accept any prompts to install additional components.

2. **Point `xcode-select` to the Xcode developer directory**  
   ```bash
   sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
   sudo xcodebuild -license accept

   This ensures `clang++` uses the full Xcode SDK (with headers like `<vector>` and `<mutex>`).

3. **Verify that `clang++` is using the XcodeDefault.xctoolchain include path**  
   ```bash
   clang++ -v -E -x c++ /dev/null
   ```
   In the “#include <...> search starts here:” section, you should see a path such as:

   /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1

   If you see that, the C++ standard-library headers are available.

4. **Install Python dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r src/requirements.txt
   ```
