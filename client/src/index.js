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

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(rootReducer)}>
    <BrowserRouter>
      <div>
        <Switch>
          <Route exact path="frontend/" component={SelectLevel} />
          <Route exact path="frontend/test" component={Login} />
          <Route exact path="frontend/posts" component={Posts} />
          <Route exact path="frontend/posts/clozes" component={PostClozes} />
          <Route exact path="frontend/user" component={UserPage} />
          <Route exact path="frontend/user/clozes" component={UserClozes} />
          <Route exact path="frontend/user/words" component={UserWords} />
          <Route exact path="frontend/user/words/study" component={UserWordsStudy} />
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
)