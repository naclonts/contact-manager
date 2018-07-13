/**
 * This module contains functions to interact with the server.
 */

/**
 * Get a list of contacts saved by the current user.
 * @return {[Object]}
 */
export async function getContacts() {
    let response = await request('contacts');
    return await response.json();
}

/**
 * Add new contact to server.
 * @param {Object} contact to add
 */
export async function addContact(contact) {
    let response = await request('contacts', 'POST', { contact });
    return await response.json();
}

/**
 * Replace the given contact on server.
 * @param  {Object} contact with updated fields
 */
export async function updateContact(contact) {
    let response = await request('contacts', 'PUT', { contact });
    return await response.json();
}

/**
 * Helper function to make HTTP requests to server.
 * @param  {String} url endpoint (after '/api/')
 * @param  {String} [method='GET']
 * @param  {Object} [body={}] JSON data to post/put/etc.
 * @return {Response}
 */
async function request(url, method='GET', body={}) {
    let apiUrl = 'http://127.0.0.1:5000/api/' + url;
    let options = {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    };

    if (method != 'GET') {
        options.body = JSON.stringify(body);
    }

    return fetch(apiUrl, options)
        .then(async (response) => {
            return response;
        });
}
