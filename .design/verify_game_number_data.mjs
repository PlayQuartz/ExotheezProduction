import assert from 'node:assert/strict'
import { fetchWlsGameNumber } from '../src/data/wls.js'
let pages = []
globalThis.fetch = async (url) => {
  pages.push(url)
  const page = Number(new URL(url).searchParams.get('page'))
  return { ok: true, json: async () => ({ page, total_pages: 2, teams: [{ sessions: page === 0 ? { a: { place: 1 }, b: { place: 2 } } : { a: { place: 1 }, c: { place: 1 } } }] }) }
}
assert.equal((await fetchWlsGameNumber('test-window')).gameNumber, 3)
assert.equal(pages.length, 2)
assert.ok(pages.every(url => url.includes('/test-window?')))
for (const wins of [0, 1, 4]) {
 globalThis.fetch = async () => ({ ok: true, json: async () => ({ page: 0, total_pages: 1, teams: [{ sessions: Object.fromEntries(Array.from({ length: wins }, (_, i) => [String(i), { place: 1 }])) }] }) })
 assert.equal((await fetchWlsGameNumber('test')).gameNumber, wins + 1)
}
globalThis.fetch = async () => ({ ok: false, status: 503 })
await assert.rejects(fetchWlsGameNumber('test'), /503/)
console.log('PASS: all pages, unique matches, zero/one/multiple wins, window id, failed response')
