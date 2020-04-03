import axios from "axios"

const ROOT_URL = "http://localhost:5005"

export const GET_POSTS = 'get_posts'
export const GET_POST_CLOZES = "get_post_clozes"
export const INCREMENT_POST_COUNT = "increment_post_count"
export const DECREMENT_POST_COUNT = "decrement_post_count"
export const SET_VIEW_NUM = "set_view_num"
export const REMOVE_GUESSED_CLOZE = "remove_guessed_cloze"

export function getPosts(viewNum, startPost) {
    const posts = axios.get(`${ROOT_URL}/posts?viewNum=${viewNum}&startPost=${startPost}`, {withCredentials: true})

    return {
        type: GET_POSTS,
        payload: posts
    }
}

export function getPostClozes(viewNum, startPost) {
    const clozes = axios.get(`${ROOT_URL}/posts/clozes?viewNum=${viewNum}&startPost=${startPost}`, {withCredentials: true})

    return {
        type: GET_POST_CLOZES,
        payload: clozes
    }
}

export function incrementPostNumber(amount) {
    console.log(amount)
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
        return c.unclozedPost != cloze.unclozedPost
    })

    return {
        type: REMOVE_GUESSED_CLOZE,
        payload: clozesMinusMarked
    }
}