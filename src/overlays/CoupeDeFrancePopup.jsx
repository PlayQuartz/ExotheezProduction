import './coupe-de-france.css'
import { consistencyStandings } from '../data/wls.js'

export function CoupeDeFrancePopup({ data }) {
  const params = new URLSearchParams(location.search)
  const positiveInteger = (value, fallback) => /^\d+$/.test(value ?? '') && Number.isSafeInteger(Number(value)) && Number(value) > 0 ? Number(value) : fallback
  const start = positiveInteger(params.get('start'), 1)
  const requestedStop = positiveInteger(params.get('stop'), start + 9)
  const stop = Math.min(Math.max(start, requestedStop), start + 9)
  const consistency = params.get('type') === 'consistency'
  const result = consistency ? consistencyStandings(data.standings) : { standings: data.standings, removedCount: 0 }
  const teams = result.standings.filter((team, index) => {
    const rank = team.rank ?? index + 1
    return rank >= start && rank <= stop
  }).slice(0, 10)
  const hasLeader = teams.length > 0 && (teams[0].rank ?? start) === 1
  const requestedQualified = positiveInteger(params.get('qualified'), null)
  const qualified = requestedQualified === null ? null : Math.max(0, requestedQualified - result.removedCount)
  const boundary = qualified === null ? -1 : teams.findIndex((team, index) =>
    (team.rank ?? start + index) === qualified)
  const dividerBeforeFirst = qualified !== null && teams.length > 0 && (teams[0].rank ?? start) === qualified + 1
  const showDivider = boundary >= 0 || dividerBeforeFirst
  const dividerTop = 51 + (boundary + 1) * 44
  const artwork = `/events/coupe-de-france-fortnite-2026/popup-leaderboard${hasLeader ? '' : '-plain'}-artwork.png`
  return <section className="cdf-popup" style={{ aspectRatio: `303 / ${showDivider ? 520 : 496}` }} aria-label={`Coupe de France ? classement des rangs ${start} ? ${stop}`}>
    <div className="cdf-popup-content" style={{ height: showDivider ? 520 : 496 }}>
      <img src={artwork} width="303" height="496" alt="Classement : rang, duo, total" style={showDivider ? { clipPath: `inset(0 0 ${496 - dividerTop}px 0)` } : undefined} />
      {showDivider && <>
        <img className="cdf-popup-lower-artwork" src={artwork} width="303" height="496" alt="" style={{ clipPath: `inset(${dividerTop}px 0 0 0)` }} />
        <div className="cdf-popup-qualified" style={{ top: dividerTop }}>TEAM QUALIFIÉ</div>
      </>}
      <ol className="cdf-popup-rows" start={start} style={dividerBeforeFirst ? { marginTop: 24 } : undefined}>{teams.map((team, index) => <li key={team.id} style={index === boundary ? { marginBottom: 24 } : undefined} className={`cdf-popup-row${(team.rank ?? start + index) === 1 ? ' is-leader' : ''}${team.dead ? ' is-dead' : ''}`} aria-label={team.dead ? 'Duo éliminé' : 'Duo en jeu'}>
        <span className="cdf-popup-rank">{String(team.rank ?? start + index).padStart(2, '0')}</span>
        <span className="cdf-popup-name" title={team.name}>{team.name}</span>
        <span className="cdf-popup-points">{team.points}</span>
      </li>)}</ol>
    </div>
  </section>
}
