FROM node:15.1.0

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y nano

RUN mkdir src

COPY ./package.json /app/
COPY ./package-lock.json /app/

RUN npm install -g @vue/cli

RUN npm install
# RUN npm update --save

# RUN npm install --save vue-template-loader webpack-stream

#COPY ./.browserslistrc /app/
#COPY ./.eslintrc.js /app/
# RUN npm install

RUN npm install axios --save
# RUN npm install jquery --save
RUN npm install bootstrap --save
RUN npm install vue-select --save
RUN npm install @fortawesome/fontawesome-svg-core --save
RUN npm install @fortawesome/free-solid-svg-icons --save
RUN npm i --save @fortawesome/vue-fontawesome@2
RUN npm i --save vuedraggable
RUN npm i --save vuelidate
RUN npm i @types/vuelidate -D
RUN npm i --save vuelidate-property-decorators
RUN npm i --save lodash
# RUN npm i --save @popperjs/core
RUN npm install vue-popperjs --save
RUN npm install bootstrap-vue@2.20.1 --save

RUN npm i pug-plain-loader pug --save
RUN npm install -D stylus-loader stylus

# RUN npm install vue-js-modal vue-flash-message --save
# RUN npm install @handsontable/vue handsontable --save
# RUN npm install vls -D --save

# RUN npm install sass-loader node-sass style-loader -D
# COPY ./vue.config.js /app/

# CMD ["npm", "run", "serve"]
