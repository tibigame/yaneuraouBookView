export async function callApi(method: string, path: string, data?: any) {
  const url = 'http://localhost:3000'
  const res = await fetch(url + path, {
    method,
    mode: 'cors',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(data)
  })
  return await res.json()
}
