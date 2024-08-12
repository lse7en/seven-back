# 

## env variables

copy .env.example to .env.rajab


## migrations
 source .env.rajab; alembic upgrade head 


## vscode
launch.json content 

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.main:create_application",
                "--factory",
                // "--reload",
                "--port",
                "4000"
            ],
            "justMyCode": false, // Set justMyCode to false
            "envFile": "${workspaceFolder}/.env.rajab"
        },
    ]
}
`