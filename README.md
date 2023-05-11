# Water Fountain with Lights and Music Show

This repository contains Python scripts for creating a mesmerizing water fountain show with synchronized lights and music. The system is based on an FPGA (Field-Programmable Gate Array) which allows for efficient real-time processing and control of the water pumps and LED strips. The scripts in this repository are responsible for extracting music features and mapping them to the water pumps and LED stripes, enabling a dynamic and captivating show.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Real-time music feature extraction, including beat detection, tempo, and frequency analysis.
- Dynamic mapping of music features to water pump intensity and LED strip colors and patterns.
- Support for a variety of music file formats.
- Customizable parameters for adapting the show to different fountain setups and preferences.

## Requirements

- Python 3.6 or higher
- FPGA board and compatible development environment
- Water pumps, LED strips, and necessary hardware for fountain setup
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository to your local machine 
2. Navigate to the repository folder and install the required Python packages:
```
cd water-fountain-lights-music-show
pip install -r requirements.txt
```

3. Configure your FPGA development environment and hardware according to the manufacturer's documentation.

## Usage

1. Customize the `config.py` file to match your hardware setup and desired show parameters.

2. Run the `main.py` script to start the water fountain show:

```
python main.py --input /path/to/your/music/file
```

3. Enjoy the synchronized water, lights, and music show!

For additional options and customization, see the script documentation or run `python main.py --help`.

## Contributing

We welcome contributions to improve this project. Please submit a pull request with your changes, or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


