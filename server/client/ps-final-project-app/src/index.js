import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import promise from "redux-promise";
import Login from "./components/login.js"
import SelectLevel from "./components/selectLevel.js"
import './index.css'

import rootReducer from "./reducers/index.js";

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(rootReducer)}>
    <BrowserRouter>
      <div>
        <Switch>
          <Route exact path="/" component={SelectLevel} />
          <Route exact path="/selectlevel" component={Login} />
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
)