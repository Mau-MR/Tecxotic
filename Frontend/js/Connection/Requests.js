export const webRequest = async (method, url, body) => {
    console.log(method,url,body)
    let response =  await fetch(url,{
        headers: {
            'Content-Type': 'application/json'
            },
        method: method,
        body: JSON.stringify(body)
    })
    let json =  await response.json
    return json
}