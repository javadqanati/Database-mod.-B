#!/usr/bin/env bash
# wait-for-it.sh adapted for Neo4j bolt

host="$1"
port="$2"
shift 2
cmd="$@"

echo "⌛ Waiting for $host:$port to be available..."
until nc -z "$host" "$port"; do
  >&2 echo "🔁 $host:$port not yet available..."
  sleep 2
done

echo "✅ $host:$port is up — starting subscriber..."
exec $cmd
