import { combineReducers } from "redux"
import PostsReducer from "./postsReducer"
import ViewNumReducer from "./viewNumReducer"
import PostCountReducer from "./postCountReducer"
import ClozeReducer from "./clozeReducer"
import SearchResultReducer from "./searchResultReducer"
import SearchTermReducer from "./searchTermReducer"
import WordReducer from "./wordReducer"

const rootReducer = combineReducers({
    posts: PostsReducer,
    clozes: ClozeReducer,
    startPost: PostCountReducer,
    viewNum: ViewNumReducer,
    searchTerm: SearchTermReducer,
    searchResult: SearchResultReducer,
    words: WordReducer
})

export default rootReducer