import axios from "axios"

const ROOT_URL = "http://localhost:5005"

export const GET_POSTS = 'get_posts'

export function getPosts(viewNum) {
    const posts = axios.get(`${ROOT_URL}/posts?viewnNum=${viewNum}`, {withCredentials: true})

    return {
        type: GET_POSTS,
        payload: posts
    }
}