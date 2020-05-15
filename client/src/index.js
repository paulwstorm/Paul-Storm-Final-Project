import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import promise from "redux-promise";
import Posts from "./components/posts.js"
import SelectLevel from "./components/selectLevel.js"
import Login from "./components/login.js"
import PostClozes from "./components/postClozes.js"
import './index.css'
import UserPage from "./components/userPage"
import UserClozes from "./components/userClozes"
import UserWords from "./components/userWords"
import UserWordsStudy from "./components/userWordsStudy"

import rootReducer from "./reducers/index.js";

const proxy = require('http-proxy-middleware')

module.exports = function(app) {
    // add other server routes to path array
    app.use(proxy(['/backend' ], { target: 'http://localhost:5000' }));
}

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(rootReducer)}>
    <BrowserRouter>
      <div>
        <Switch>
          <Route exact path="/" component={SelectLevel} />
          <Route exact path="/test" component={Login} />
          <Route exact path="/posts" component={Posts} />
          <Route exact path="/posts/clozes" component={PostClozes} />
          <Route exact path="/user" component={UserPage} />
          <Route exact path="/user/clozes" component={UserClozes} />
          <Route exact path="/user/words" component={UserWords} />
          <Route exact path="/user/words/study" component={UserWordsStudy} />
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
)