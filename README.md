# LimaKiloBot
Proof of concept for the Lima Kilo DCS Community.

![image](https://user-images.githubusercontent.com/40549750/149166279-f3b7a314-367c-4f0a-82e6-bf3136b52a6f.png)

## Currently supported slash commands:
- `/gci <state:str> <notes:str>`
- `/flight` 
  - `/listing <show:bool>` 
  - `/lff <aircraft:str> <notes:str>`
  - `/join <flight:str> <aircraft:str>`
  - `/retire`
  - `/leave`
  - `/status <show:bool>`

## Legacy Commands (Soon to be replaced by slash commands)
- `lso`
- `info`

## Requirements
- Poetry
- Python 3.9.6
- nextcord 
- python-dotenv

## Required Heroku Hosting Buildpacks
- https://github.com/moneymeets/python-poetry-buildpack.git
- heroku/python
