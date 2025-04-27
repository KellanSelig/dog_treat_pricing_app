# Left to do

1. Finish converters [DONE]
2. Run dog treat w/t AI setup
3. Test
4. client API + test
5. Front end

## Run Server

```bash
PYTHONPATH=. uv run python backend/grpc_service/main.py
```

## Generate Servicer

```bash
sh code_gen.sh
```

## GRPCurl

```bash
grpcurl -plaintext localhost:50051 describe
```
