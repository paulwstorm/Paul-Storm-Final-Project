import { WORD_SEARCH } from "../actions/index.js"

function compare(a, b) {
    const simplifiedA = a.simplified.length;
    const simplifiedB = b.simplified.length;
  
    let comparison = 0;
    if (simplifiedA > simplifiedB) {
      comparison = 1;
    } else if (simplifiedA < simplifiedB) {
      comparison = -1;
    }
    return comparison;
  }

export default function(state = [], action) {
    switch(action.type) {
        case WORD_SEARCH:
            state = action.payload.data
            return state.slice(0,5)
        default:
            return state
    }
}