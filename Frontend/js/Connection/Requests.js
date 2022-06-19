export const webRequest = async (method, url, body) => {
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
export const requestWithBLOB = async (method, url, body) =>{
    let response =  await fetch(url,{
        headers: {
            'Content-Type': 'application/json'
        },
        method: method,
        body: JSON.stringify(body)
    })
    const blob = await response.blob()
    return window.URL.createObjectURL(blob)
}