const apiPort = "8000"

const apiURL = (path: string) => { // transform relative url to api url
    const url = new URL(path, window.location.origin)
    url.port = apiPort
    return url
}

export default apiURL
