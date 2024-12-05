# ampsorter
Motor program spike sorting GUI/application built on PyQt6
# AMPS Spike Sorting App

## Installation

### Windows
1. Navigate to the `dist` folder in the GitHub repository.
2. Download `amps.exe`.

### Linux and macOS
1. Open the terminal and navigate to the directory where you want to house the AMPS code files.
2. Run: git clone https://github.com/LeoJW/ampsorter.git
3. Open the cloned repository in Visual Studio Code.
4. Create a virtual environment (venv) and select the most up-to-date version of Python.
5. Install the required dependencies: pip install numpy scipy h5py dill PyQt6 pyqtgraph

Alternatively, you can use a translator such as Wine to run the `.exe` file on your system.

---

## Usage

### Run the Code

#### If you cloned the whole repo:
1. Open the repository in the virtual environment you created.
2. Locate `amps.py` and run the code using the "Run" button in the top right corner of Visual Studio Code.

#### If you downloaded the `.exe` file:
1. Run `amps.exe`.

---

### Open File
1. The program will open a new window with a "File" tab in the top left corner.
2. Click on the "File" tab, then select "Open" from the dropdown menu.
3. Navigate to the file containing the trial data and select it.
- **Keyboard Shortcut**: `Ctrl + O`.
4. After the first time, you can reuse the same data by selecting "Load last session."
- **Keyboard Shortcut**: `Ctrl + L`.

**Preferred File Formats**:
- **`.mat`**: 
- Contains a struct with two fields:
 - `struct.data`: An array where rows represent sample data and columns represent channel names.
 - `struct.channelNames`: A list of channel names (capitalized muscle names, all other fields lowercase).
- **`.h5`**: 
- Contains two datasets:
 - `['data']`: Rows are the channel names (capitalized); columns are muscle data.
 - `['names']`: A collection of channel names (capitalized).

**Other Accepted File Formats**:
- `.mat`: Pre-2022 formats.

---

### Select Trial and Muscles
1. On the left, all trials and muscles in the file are listed.
2. Select a trial and muscle(s) to analyze by clicking and dragging to highlight them.
- To select specific muscles, hold `Ctrl` and click on the desired muscles.

Graphs of the selected muscles' traces will appear in the bottom half of the screen.  
- Click on a trace to make it the active trace.  
- **Active Trace**: Colored white instead of the default color.
- **Keyboard Shortcuts**: Use `Ctrl + Up Arrow` and `Ctrl + Down Arrow` to switch between active traces.

---

### Add Filters
1. Go to the "Filters" tab.
2. Select the filter type and adjust its parameters.
3. Apply the filter to the active trace:
- **Keyboard Shortcut**: `F`.

---

### Setting Spike Threshold
1. Select a graph from the bottom of the screen.
2. Adjust the threshold for spike detection:
- **Keyboard Shortcuts**: 
  - Use the `Up Arrow` and `Down Arrow` keys for coarse adjustments.
  - Hold `Alt` for finer adjustments.
3. Go to the "Detection" tab and click "Detect Spikes" or press `Space`.
4. Use "Autodetect" to apply detection across all muscles if the initial results look correct.

---

### Principal Component Analysis (PCA)
1. Navigate to the "PC" tab.
2. Enter the desired PC values for the x-axis and y-axis (range: 1–12).

---

### Spike Selection
1. To focus on specific spikes:
- Click and drag over the desired spikes in the PCA viewer while holding a number key to change their color.
- The new color will update across all spike representations.

---

### Other Settings
1. Go to the "Preferences" tab in the top left corner.
2. A new box will open, allowing you to modify settings like:
- Waveform length.
- Alignment settings.
- Dead time between samples.
- Fractional pre-alignment.

---

### Keyboard Shortcuts

| Shortcut                  | Action                                      |
|---------------------------|---------------------------------------------|
| `Ctrl + O`                | Open file                                  |
| `Ctrl + L`                | Load previously opened file                |
| `Ctrl + S`                | Save                                       |
| `Ctrl + Up/Down Arrow`    | Change active trace                        |
| `Ctrl + Shift + A`        | Automatically set thresholds               |
| `Up/Down Arrow`           | Move threshold up/down                     |
| `Alt + Up/Down Arrow`     | Fine-adjust threshold                      |
| `F`                       | Apply filter                               |
| `Ctrl + Shift + F`        | Autodetect filters                         |
| `Space`                   | Detect spikes                              |
| `Shift + Space`           | Undetect spikes                            |
| `Ctrl + Shift + L`        | Autodetect spikes                          |
| `Ctrl + Shift + I`        | Invalidate crosstalk                       |
| `Shift + Left/Right`      | Pan left/right                             |
| `Shift + Up/Down`         | Zoom in/out                                |
| `Ctrl + Shift + M`        | Match times and samples                    |
| `Ctrl + Left/Right`       | Switch between trials                      |
| `I/O/P`                   | Change PC view X (0–2)                     |
| `J/K/L`                   | Change PC view Y (0–2)                     |

---

## Known Issues
- **Scrolling Through Highlights**:
- Using `Ctrl + Up/Down` navigates through all muscles, even unhighlighted ones, if there is a gap between selected muscles.
- **Reverse Order**:
- Graphs appear in reverse order compared to the muscle selection section, which may confuse users.
- **Un-highlighting Issue**:
- Pressing `Ctrl + Up` when the active trace is the highest un-highlights it, while `Ctrl + Down` on the lowest trace does nothing.

---

## Authors
- Leo Wood
- Joshua Davenport
- Max Chen

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
