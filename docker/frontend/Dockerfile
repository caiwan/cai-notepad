# Build static html packages w/ NPM
FROM node:11-alpine as build
RUN apk update && apk add bash
ADD ../../client /client
WORKDIR /client
RUN npm install && \
  npm run build

FROM nginx:1.13-alpine
COPY --from=build /client/dist/* /frontend/
COPY nginx.conf /etc/nginx/nginx.conf
