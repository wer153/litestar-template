#!/bin/bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=test -p 5432:5432 -d postgres:latest
uv run sync && uv run prisma migrate dev --name test
