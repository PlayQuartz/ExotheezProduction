// Sessions belong to teams, so a duo/trio victory counts once per match.
export async function fetchWlsGameNumber(leaderboardId, signal, includeStandings = false) {
  const wins = new Set()
  const allTeams = []
  let totalPages = 1
  for (let page = 0; page < totalPages; page++) {
    const response = await fetch(`https://api.wls.gg/v5/leaderboards/${encodeURIComponent(leaderboardId)}?page=${page}`, { cache: 'no-store', signal })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const payload = await response.json()
    if (!Array.isArray(payload.teams) || payload.page !== page || !Number.isInteger(payload.total_pages) || payload.total_pages < 1) throw new Error('Invalid WLS leaderboard')
    if (page === 0) totalPages = payload.total_pages
    if (payload.total_pages !== totalPages) throw new Error('WLS pagination changed during update')
    allTeams.push(...payload.teams)
    for (const team of payload.teams) {
      for (const [matchId, session] of Object.entries(team.sessions ?? {})) {
        if (session.place === 1) wins.add(matchId)
      }
    }
  }
  const standings = includeStandings
    ? normalizeWls({ teams: allTeams, page: 0, total_pages: 1 }, 0, allTeams.length).standings.map((team, index) => ({
      ...team,
      dead: Object.keys(allTeams[index].sessions ?? {}).length > wins.size,
    }))
    : []
  return { gameNumber: wins.size + 1, standings }
}

export function consistencyStandings(standings) {
  const winners = new Set(standings.filter(team => team.hasWin).map(team => team.id))
  return {
    removedCount: winners.size,
    standings: standings.filter(team => !team.hasWin).map((team, index) => ({ ...team, rank: index + 1 })),
  }
}

export function normalizeWls(payload, displayPage, count = 10) {
  if (!Array.isArray(payload.teams) || !Number.isInteger(payload.total_pages) || payload.total_pages < 1) throw new Error('Invalid WLS leaderboard')
  const offset = (displayPage % 10) * 10
  const apiPage = Math.floor(displayPage / 10)
  if (payload.page !== apiPage) throw new Error('Unexpected WLS page')
  const teams = payload.teams.slice(offset, offset + count)
  const standings = teams.map(team => ({
    id: String(team.id),
    // Sort displayed player names alphabetically in every overlay and refresh.
    name: Object.entries(team.members ?? {})
      .sort(([keyA, a], [keyB, b]) => {
        const nameA = a.ingame_name || a.name || ''
        const nameB = b.ingame_name || b.name || ''
        const alphabetical = nameA.localeCompare(nameB, 'fr', { sensitivity: 'base' })
        if (alphabetical) return alphabetical
        const exact = nameA.localeCompare(nameB, 'fr', { sensitivity: 'variant' })
        if (exact) return exact
        const idA = String(a.id ?? keyA)
        const idB = String(b.id ?? keyB)
        return idA < idB ? -1 : idA > idB ? 1 : 0
      })
      .map(([, member]) => member.ingame_name || member.name).filter(Boolean).join(' - ') || 'Unknown duo',
    rank: team.place,
    points: team.points,
    hasWin: Object.values(team.sessions ?? {}).some(session => session.place === 1),
    eliminations: Object.values(team.sessions ?? {}).reduce((sum, session) => sum + (session.kills ?? 0), 0),
  }))
  return {
    // This endpoint has no broadcast game number. Zero means unconfigured.
    gameNumber: 0,
    standings,
    pagination: { page: displayPage, hasPrevious: displayPage > 0, hasNext: offset + 10 < payload.teams.length || apiPage + 1 < payload.total_pages },
  }
}
