import { events } from './events.js'
import { layouts } from './overlays/registry.jsx'
import { Overlay } from './data/Overlay.jsx'
import './App.css'

export default function App() {
  const path = location.pathname.replace(/\/+$/, '') || '/'
  if (path === '/') return null

  const match = path.match(/^\/overlays\/([^/]+)\/([^/]+)$/)
  const event = match && events[match[1]]
  const type = match?.[2]
  if (event && Object.hasOwn(layouts, type) && Object.hasOwn(layouts[type], event.layouts[type])) {
    return <Overlay event={event} type={type} />
  }
  return null
}
