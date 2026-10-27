import assert from 'node:assert/strict'
import { normalizeWls, fetchWlsGameNumber } from '../src/data/wls.js'
const a = { id: '90071992547409931', ingame_name: 'Alpha' }
const b = { id: '90071992547409932', ingame_name: 'Beta' }
const payload = members => ({ teams: [{ id: 'duo', place: 1, points: 10, members }], page: 0, total_pages: 1 })
const first = payload({ [b.id]: b, [a.id]: a })
const second = payload({ [a.id]: a, [b.id]: b })
assert.equal(normalizeWls(first, 0).standings[0].name, 'Alpha - Beta')
assert.equal(normalizeWls(second, 0).standings[0].name, 'Alpha - Beta')
globalThis.fetch = async () => ({ ok: true, json: async () => first })
assert.equal((await fetchWlsGameNumber('test', undefined, true)).standings[0].name, normalizeWls(second, 0).standings[0].name)
console.log('PASS: reordered members, large IDs, popup/leaderboard consistent names')
