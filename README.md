# SAI3_Chatbot
Group E

C++ wird benötigt als Code interpreter


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
   - (If you prefer Conda, you could do something like `conda create -n rag-chatbot python=3.10` and then `conda activate rag-chatbot`.)

---

## Installation (macOS)

On macOS, a full C++ toolchain with standard‐library headers is required. You must install Xcode (or at least the Xcode SDK) before proceeding:

1. **Install Xcode from the App Store**  
   - Open the App Store, search for “Xcode,” and click **Get** (or “Update” if it’s already installed).  
   - Once it’s finished downloading, launch Xcode at least once and accept any prompts to install additional components.

2. **Point `xcode-select` to the Xcode developer directory**  
   ```bash
   sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
   sudo xcodebuild -license accept
