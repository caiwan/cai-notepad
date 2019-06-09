# ---
# Build static html packages w/ NPM
FROM node:11-alpine as frontend-build
RUN apk update && apk add bash
ADD ./frontend /frontend
WORKDIR /frontend
RUN npm install && \
  npm run build

# ---

FROM nginx:alpine as frontend
EXPOSE 8081
COPY --from=frontend-build /frontend/dist/ /usr/share/nginx/html/
COPY ./docker/nginx.default.conf /etc/nginx/conf.d/default.conf
