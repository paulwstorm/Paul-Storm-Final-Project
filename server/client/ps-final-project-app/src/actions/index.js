import axios from "axios"

const ROOT_URL = "http://localhost:5005"

export const GET_POST = 'get_posts'

export function getPosts(viewNum) {
    const posts = axios.get(`${ROOT_URL}/posts?viewnNum=${viewNum}`)
    .catch((error) => {
        if (error.response) {
            alert(error)
        }
    })

    return {
        type: GET_POST,
        payload: posts
    }
}