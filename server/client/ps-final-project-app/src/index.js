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

import rootReducer from "./reducers/index.js";

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
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
)