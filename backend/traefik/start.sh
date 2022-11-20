docker run -d -p 80:80 -p 443:443 -v $PWD/traefik.toml:/traefik.toml -v /var/run/docker.sock:/var/run/docker.sock --name traefik --network traefik traefik:2.6


docker run -d \
-l traefik.http.routers.lsp.rule=Host\(\`testid.lsp.localhost\`\) \
-l traefik.http.routers.lsp.service=lsp-service \
-l traefik.http.services.lsp-service.loadbalancer.server.port=30000 \
-l traefik.http.routers.debug.rule=Host\(\`testid.debug.localhost\`\) \
-l traefik.http.routers.debug.service=debug-service \
-l traefik.http.services.debug-service.loadbalancer.server.port=30005 \
--network traefik_default python_lsp