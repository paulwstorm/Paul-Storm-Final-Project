import { combineReducers } from "redux"
import PostsReducer from "./postsReducer"
import ViewNumReducer from "./viewNumReducer"
import PostCountReducer from "./postCountReducer"
import ClozeReducer from "./clozeReducer"

const rootReducer = combineReducers({
    posts: PostsReducer,
    clozes: ClozeReducer,
    startPost: PostCountReducer,
    viewNum: ViewNumReducer
})

export default rootReducer