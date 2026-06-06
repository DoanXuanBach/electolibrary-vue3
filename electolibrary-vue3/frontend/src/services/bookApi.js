const API_URL = '/api/books'

async function handleResponse(response) {
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || 'Ошибка запроса к серверу')
  }
  return response.status === 204 ? null : response.json()
}

export async function getBooks() {
  const response = await fetch(API_URL)
  return handleResponse(response)
}

export async function getBook(id) {
  const response = await fetch(`${API_URL}/${id}`)
  return handleResponse(response)
}

export async function createBook(formData) {
  const response = await fetch(API_URL, {
    method: 'POST',
    body: formData
  })
  return handleResponse(response)
}

export async function updateBook(id, formData) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    body: formData
  })
  return handleResponse(response)
}

export async function deleteBook(id) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: 'DELETE'
  })
  return handleResponse(response)
}
