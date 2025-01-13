# AMPS (Assisted Motor Program Sorting)
Insect EMG and motor program spike sorting GUI/application built on PyQt6

NOTE: This is home-cooked, just-like-your-mom-used-to-make software. I made it for my own purposes, and while I'm happy to support more users, there are some lingering bugs, and it isn't packaged through pip or conda. Installation requires either downloading and running the code locally, or downloading an `.exe` file provided. I promise there's probably not a virus in there!

## Installation

### Run Locally: MacOS, Linux, Windows
1. Open the terminal/shell and navigate to the directory where you want to house the AMPS code files. On Windows you can use git bash for this
2. Run: `git clone https://github.com/LeoJW/ampsorter.git`
4. Create a virtual environment (venv) in the `ampsorter` directory (this can be done in terminal as shown [here](https://docs.python.org/3/library/venv.html) or in an editor like VS Code as shown [here](https://code.visualstudio.com/docs/python/environments)) and select the most up-to-date version of Python.
5. Install the required dependencies: `pip install numpy scipy h5py dill PyQt6 pyqtgraph`


### Run Executable: Primarily Windows 
1. Navigate to the dist folder in this Github repository
2. Download `amps.exe`

For macOS/Linux, you can potentially use a translator such as Wine to run the `.exe` file on your system. We can compile standalone executables for Linux and MacOS, or whatever machine you'd like if we can find a similar machine and run the compilation. 

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
This program expects one of two specific file formats. In both formats, **only channel names which start with a capital letter are read and displayed**. The convention is that muscle channels are named starting with a capital letter, everything else with lowercase letter. 

**`.h5`**: 
- Contains two datasets:
- `['data']`: Rows are the channel names; columns are muscle data.
- `['names']`: A collection of channel names. Only names starting with a capital letter are treated as muscles.

**`.mat`**: 
 - Contains a struct with two fields:
 - `struct.data`: An array where rows represent sample data and columns represent channel names.
 - `struct.channelNames`: A list of channel names (capitalized muscle names, all other fields lowercase).

**Other Accepted File Formats**:
- `.mat`: Pre-2022 formats. Consider this undocumented back-compatibilty for an old Sponberg lab format

---

### Select Trial and Muscles
1. On the left, all trials and muscles in the file are listed.
2. Select a trial and muscle(s) to analyze by clicking and dragging to highlight them.
- To select specific muscles, hold `Ctrl` (`Cmd` on MacOS) and click on the desired muscles.

Graphs of the selected muscles' traces will appear in the bottom half of the screen.  
- Click on a trace to make it the active trace.  
- **Active Trace**: Colored white instead of the default color.
- **Keyboard Shortcuts**: Use `Ctrl + Up Arrow` and `Ctrl + Down Arrow` to switch between active traces. Note that all shortcuts with `Ctrl` will use `Cmd` instead on MacOS

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
Useful for picking out clusters, invalidating or sorting groups of spikes with certain properties
- Each point displayed is a spike from the currently selected channel in the currently selected trial
- X and Y axes by default display the projection (scores) of each spike on PCs 1 and 2
- Which PC is displayed on each axis can be changed through the PCA tab or via keyboard shortcut
- Clicking and dragging over a selection of spikes will "invalidate" those spikes in all screens
- Clicking and dragging, but pressing any number 0-9 before releasing, will instead assign those spikes to a "unit", and color them on all screens accordingly

---

### Spike Selection
Spikes can be selected in both PCA and bottom spike views
- Click and drag over the desired spikes in either viewer. Releasing will toggle selected spikes between "valid" (normal) and "invalid" (greyed out) tags
- Click and drag, but pressing any number key 0-9 before release, will instead assign selected spikes to a "unit", and color on all screens accordingly

---

### Other Settings
1. Go to the "Preferences" tab in the top left corner (`Ctrl + ,`, `Cmd + ,` on Mac)
2. A new box will open, allowing you to modify the following:

| Setting            |                    |
|------------------  |--------------------|
| Waveform length    | How long, in samples, of a snippet is extracted for each spike |
| Align at           | Whether to choose spike time as time at peak, or time at which threshold was crossed |
| Dead time          | How many samples after a spike is detected before another can be detected |
| Fraction pre-align | Fraction of spike waveform pre-alignment point (peak or threshold crossing) |

---

### Keyboard Shortcuts

On MacOS all `Ctrl` shortcuts are instead `Cmd`

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

Written by Leo Wood

Additional support from Joshua Davenport, Max Chen

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
