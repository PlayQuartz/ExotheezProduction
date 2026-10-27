// Each event selects its own designs while all its overlays share one data URL.
export const events = {
  'coupe-de-france-fortnite-2026': {
    id: 'coupe-de-france-fortnite-2026',
    name: 'Coupe de France Fortnite 2026',
    accent: '#13f1f0',
    dataUrl: '/data/coupe-de-france-fortnite-2026.json',
    dataSource: 'wls',
    leaderboardId: '0-0000-888411444641538048',
    layouts: { leaderboard: 'coupe-de-france-top10', 'game-number': 'coupe-de-france-game-number', 'popup-leaderboard': 'coupe-de-france-popup' },
  },
  'event-x': {
    id: 'event-x', name: 'Event X', accent: '#c2ff63', dataUrl: '/data/event-x.json',
    layouts: { leaderboard: 'default', 'game-number': 'default', 'popup-leaderboard': 'compact' },
  },
  'event-y': {
    id: 'event-y', name: 'Event Y', accent: '#87bfff', dataUrl: '/data/event-y.json',
    layouts: { leaderboard: 'default', 'game-number': 'default', 'popup-leaderboard': 'compact' },
  },
}
