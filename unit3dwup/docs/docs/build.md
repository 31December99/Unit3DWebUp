## Frontend build

```bash
flutter pub get
flutter build web --release --wasm
```

---

## Backend build

```bash
docker-compose -f build.yml build --no-cache
docker-compose up
```

---

## Docker Hub

```bash
docker login

docker tag unit3dwebup-backend:latest parzival2025/backend_app:x.y.z
docker tag unit3dwebup-frontend:latest parzival2025/frontend_app:x.y.z

docker push parzival2025/backend_app:x.y.z
docker push parzival2025/frontend_app:x.y.z
```