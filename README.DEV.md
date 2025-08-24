## AutoGPT setup
https://docs.agpt.co/platform/getting-started/

1. change directory to **autogpt_platform**
2. run command
```
docker compose up -d --build
```

## AutoGPT startup

### Minimal startup
```
docker compose up -d
```

### Startup with supabase studio(for deveopment)
```
docker compose --profile local up -d
```

## For DEV
https://dev-docs.agpt.co/platform/getting-started/#development

### Server Dev
- change directory to **autogptplatform**
Start prerequisites servers like supabase, redis, RabitMQ etc.
> docker compose --profile local up deps --build --detach
- change directory to **autogptplatform/backend**
> poetry run app

#### Block test
> `poetry run pytest backend/blocks/test/test_block.py -s`

#### Formatting & Linting
> formatting: `poetry run format`
> Linting: `poetry run lint`

### Frontend Dev
> Generate the API client: `pnpm generate:api-client`
> Run the frontend application: `pnpm dev`

#### Formatting & Linting
> Formatting: `pnpm format`
> Linting: `pnpm lint`

#### Testing
> pnpm test

#### 分步启动
1. DatabaseManager
poetry run db
2. Scheduler
poetry run scheduler
3. NotificationManager
poetry run notification
4. WebSocketSerer
poetry run ws
5. AgentServer()
poetry run rest
6. ExecutionManager()
poetry run executor

## Supabase Studio

Url: http://localhost:8000  
UserName: supabase  
password: this_password_is_insecure_and_should_be_updated  

(defined in autogpt_platform/db/docker/docker-compose.yml)

## Others
Best practice for SSRF prevention:  
https://dev-docs.agpt.co/platform/new_blocks/#using-the-secure-requests-wrapper

rest api dock:
http://localhost:8006/docs
http://localhost:8006/redoc

## Docker私有仓库

`localhost:5000`

### 私有仓库列表
http://localhost:5000/v2/_catalog

### 私有仓库操作
以ubuntu为例：  
- docker pull ubuntu:20.04
- docker tag ubuntu:20.04 localhost:5000/ubuntu:20.04
- docker push localhost:5000/ubuntu:20.04

详细操作说明：  
https://distribution.github.io/distribution/about/deploying/

https://yeasy.gitbook.io/docker_practice/repository/registry


## AutoGPT API Key
agpt_0upJLyBVlcFn9FFpHLTLUY4dQ5_VfATliISEKdtAWAs
