import axios from "axios"

const ROOT_URL = "http://localhost:5005"

export const GET_POSTS = 'get_posts'
export const GET_POST_CLOZES = "get_post_clozes"
export const INCREMENT_POST_COUNT = "increment_post_count"
export const DECREMENT_POST_COUNT = "decrement_post_count"
export const SET_VIEW_NUM = "set_view_num"
export const REMOVE_GUESSED_CLOZE = "remove_guessed_cloze"
export const WORD_SEARCH = "word_search"
export const NEW_SEARCH_TERM = "new_search_term"
export const GET_USER_CLOZES = "get_users_clozes"
export const GET_WORDS = "get_words"

export function getPosts(viewNum, startPost) {
    const posts = axios.get(`${ROOT_URL}/posts?viewNum=${viewNum}&startPost=${startPost}`, {withCredentials: true})

    return {
        type: GET_POSTS,
        payload: posts
    }
}

export async function getPostClozes(viewNum, startPost) {
    const clozes = await axios.get(`${ROOT_URL}/posts/clozes?viewNum=${viewNum}&startPost=${startPost}`, {withCredentials: true})

    return {
        type: GET_POST_CLOZES,
        payload: clozes
    }
}

export function getUserClozes(viewNum, startPost, view) {
    const userClozes = axios.get(`${ROOT_URL}/user/clozes?viewNum=${viewNum}&startPost=${startPost}&view=${view}`, {withCredentials: true})

    return {
        type: GET_USER_CLOZES,
        payload: userClozes
    }
}

export async function getWords(viewNum, startPost, view) {
    const words = await axios.get(`${ROOT_URL}/user/words?viewNum=${viewNum}&startPost=${startPost}`, {withCredentials: true})

    console.log(`${ROOT_URL}/user/clozes?viewNum=${viewNum}&startPost=${startPost}&view=${view}`)
    return {
        type: GET_WORDS,
        payload: words
    }
}

export function incrementPostNumber(amount) {
    return {
        type: INCREMENT_POST_COUNT,
        payload: amount
    }
}

export function decrementPostNumber(amount) {
    return {
        type: DECREMENT_POST_COUNT,
        payload: amount
    }
}

export function markClozeCorrect(mark, cloze, clozes) {
    let markedCloze = cloze
    markedCloze.lastAttempt = mark
    markedCloze.lastAttemptDate = new Date()

    const postMarkedCloze = axios.post(`${ROOT_URL}/posts/clozes`, markedCloze, {withCredentials: true})

    let clozesMinusMarked = clozes.filter(c => {
        return c.postContent != cloze.postContent
    })

    return {
        type: REMOVE_GUESSED_CLOZE,
        payload: clozesMinusMarked
    }
}

export function addClozeToUser(cloze) {
    let markedCloze = cloze
    markedCloze.lastAttempt = "incorrect"
    markedCloze.lastAttemptDate = new Date()
    markedCloze.postClozedTokenizedContent = cloze.postTokenizedContent
    markedCloze.multipleChoiceWords = []
    markedCloze.removedWord = ""

    const postMarkedCloze = axios.post(`${ROOT_URL}/posts/clozes`, markedCloze, {withCredentials: true})

    return postMarkedCloze 
}

export function wordSearch(word) {
    const searchResult = axios.get(`${ROOT_URL}/wordsearch?query=${word}`, {withCredentials: true})

    return {
        type: WORD_SEARCH,
        payload: searchResult
    }

}

export function addWordToUserDict(word) {
    const addWord = axios.put(axios.post(`${ROOT_URL}/addWordToDict`, word, {withCredentials: true}))

    return addWord
}

export function newSearchTerm(searchTerm) {
    return {
        type: NEW_SEARCH_TERM,
        payload: searchTerm
    }
}