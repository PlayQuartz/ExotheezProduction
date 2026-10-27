import { useEffect, useState } from 'react'
import { layouts } from '../overlays/registry.jsx'
import { normalizeWls, fetchWlsGameNumber, consistencyStandings } from './wls.js'

function validData(data) {
  return data && Number.isInteger(data.gameNumber) && data.gameNumber >= 0 && Array.isArray(data.standings) && data.standings.every(t => typeof t.id === 'string' && typeof t.name === 'string' && Number.isFinite(t.points) && (t.eliminations === undefined || (Number.isInteger(t.eliminations) && t.eliminations >= 0))) && new Set(data.standings.map(t => t.id)).size === data.standings.length
}
export function Overlay({ event, type }) {
  const [data, setData] = useState(null)
  const [requestedPage, setRequestedPage] = useState(0)
  const params = new URLSearchParams(location.search)
  const leaderboardId = params.get('id') || event.leaderboardId
  const isGameNumber = event.layouts[type] === 'coupe-de-france-game-number'
  const isPopup = event.layouts[type] === 'coupe-de-france-popup'
  const isFullFrameLeaderboard = event.layouts[type] === 'coupe-de-france-top10'
  const isConsistencyLeaderboard = event.layouts[type] === 'coupe-de-france-top10' && params.get('type') === 'consistency'
  const forceValue = params.get('forceCurrentGame')
  const forceNumber = Number(forceValue)
  const forcedGame = /^\d+$/.test(forceValue ?? '') && Number.isSafeInteger(forceNumber) && forceNumber > 0 ? forceNumber : null
  const [scale, setScale] = useState(() => (isFullFrameLeaderboard ? Math.max : Math.min)(innerWidth / 1920, innerHeight / 1080))
  useEffect(() => {
    const resize = () => setScale((isFullFrameLeaderboard ? Math.max : Math.min)(innerWidth / 1920, innerHeight / 1080))
    resize()
    addEventListener('resize', resize)
    return () => removeEventListener('resize', resize)
  }, [isFullFrameLeaderboard])
  useEffect(() => {
    if (isGameNumber && forcedGame !== null) return
    let stopped = false
    let timer
    let controller
    async function refresh() {
      controller = new AbortController()
      const timeout = setTimeout(() => controller.abort(), 12000)
      try {
        if (isGameNumber || isPopup || isConsistencyLeaderboard) {
          const next = await fetchWlsGameNumber(leaderboardId, controller.signal, isPopup || isConsistencyLeaderboard)
          if (isConsistencyLeaderboard) {
            const filtered = consistencyStandings(next.standings).standings
            const lastPage = Math.max(0, Math.ceil(filtered.length / 10) - 1)
            const page = Math.min(requestedPage, lastPage)
            next.standings = filtered.slice(page * 10, (page + 1) * 10)
            next.pagination = { page, hasPrevious: page > 0, hasNext: page < lastPage }
          }
          if (!stopped) setData(next)
          return
        }
        const source = event.dataSource === 'wls'
          ? `https://api.wls.gg/v5/leaderboards/${encodeURIComponent(leaderboardId)}?page=${Math.floor(requestedPage / 10)}`
          : event.dataUrl
        const response = await fetch(source, { cache: 'no-store', signal: controller.signal })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const payload = await response.json()
        const next = event.dataSource === 'wls' ? normalizeWls(payload, requestedPage) : payload
        if (!validData(next)) throw new Error('Invalid event data')
        if (!stopped) setData(next)
      } catch (error) {
        if (!stopped) console.warn(`[${event.id}] Data update failed:`, error.message)
      } finally {
        clearTimeout(timeout)
        if (!stopped) timer = setTimeout(refresh, event.dataSource === 'wls' ? 15000 : 2000)
      }
    }
    refresh()
    return () => { stopped = true; clearTimeout(timer); controller?.abort() }
  }, [event, isGameNumber, isPopup, isConsistencyLeaderboard, forcedGame, leaderboardId, requestedPage])
  const Layout = layouts[type][event.layouts[type]]
  const displayData = isGameNumber && forcedGame !== null
    ? { gameNumber: forcedGame, standings: [] }
    : data ?? { gameNumber: isGameNumber ? 1 : 0, standings: [] }
  return <div className={`viewport${isFullFrameLeaderboard ? ' viewport-cdf-leaderboard' : ''}`}><div className="canvas" style={{ transform: `${isFullFrameLeaderboard ? 'translate(-50%, -50%) ' : ''}scale(${scale})`, '--accent': event.accent }}><Layout event={event} data={displayData} onPageChange={setRequestedPage} /></div></div>
}

