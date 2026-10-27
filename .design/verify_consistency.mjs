import assert from 'node:assert/strict'
import { consistencyStandings, fetchWlsGameNumber } from '../src/data/wls.js'
const teams=Array.from({length:30},(_,i)=>({id:String(i+1),place:i+1,points:100-i,members:{},sessions: i===2 ? {a:{place:1},b:{place:1}} : i===28 ? {c:{place:1}} : {}}))
globalThis.fetch=async url=>{const page=Number(new URL(url).searchParams.get('page'));return {ok:true,json:async()=>({teams:teams.slice(page*15,(page+1)*15),page,total_pages:2})}}
const data=await fetchWlsGameNumber('test',undefined,true)
const result=consistencyStandings(data.standings)
assert.equal(result.removedCount,2)
assert.equal(result.standings.length,28)
assert.equal(result.standings[2].id,'4')
assert.equal(result.standings[2].rank,3)
assert.equal(result.standings[22].rank,25-result.removedCount)
assert.equal(data.standings[2].rank,3)
console.log('PASS: winners across pages excluded, repeat winner counts once, ranks close gaps, input unchanged')
