/*
export function someGetter (state) {
}
*/

export function getQuery(state) {
    return state.global_query;
}

export function getFirstNodeSid(state) {
    return state.first_node_sid;
}