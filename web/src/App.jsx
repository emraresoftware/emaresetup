import { useState, useEffect } from 'react'

const API = '/api'

function useApi(path) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const refetch = () => {
    setLoading(true)
    fetch(`${API}${path}`)
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(setData)
      .catch(e => setError(String(e)))
      .finally(() => setLoading(false))
  }

  useEffect(refetch, [path])
  return { data, loading, error, refetch }
}

// ─── Dashboard ─────────────────────────────────────────────────
function Dashboard() {
  const { data: stats, loading } = useApi('/stats')
  const { data: modules } = useApi('/modules')

  if (loading) return <div className="loading">Yükleniyor...</div>

  return (
    <>
      <div className="stat-grid">
        <div className="stat-card">
          <div className="number">{stats?.total_modules || 0}</div>
          <div className="label">Toplam Modül</div>
        </div>
        <div className="stat-card">
          <div className="number">{stats?.total_code_lines || 0}</div>
          <div className="label">Kod Satırı</div>
        </div>
        <div className="stat-card">
          <div className="number">{stats?.total_test_files || 0}</div>
          <div className="label">Test Dosyası</div>
        </div>
        <div className="stat-card">
          <div className="number">{stats?.providers_available?.length || 0}</div>
          <div className="label">AI Sağlayıcı</div>
        </div>
      </div>

      <h2 style={{ marginBottom: '1rem' }}>📦 Modüller</h2>
      <div className="grid">
        {modules?.map(mod => (
          <div className="card" key={mod.name}>
            <h3>
              {mod.has_code ? '✅' : '⚠️'} {mod.name}
            </h3>
            <div className="meta">
              <span className="badge info">{mod.type}</span>
              {' '}
              {mod.version && <span className="badge success">v{mod.version}</span>}
              {' '}
              {mod.has_tests ? <span className="badge success">tested</span> : <span className="badge warning">no test</span>}
            </div>
            <div className="meta" style={{ marginTop: '0.5rem' }}>
              {mod.registered_at?.slice(0, 19)}
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

// ─── Modules ───────────────────────────────────────────────────
function Modules() {
  const { data: modules, loading, refetch } = useApi('/modules')
  const [creating, setCreating] = useState(false)
  const [form, setForm] = useState({ name: '', module_type: 'standard_module', description: '' })

  const handleCreate = async () => {
    if (!form.name) return
    setCreating(true)
    try {
      await fetch(`${API}/modules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      setForm({ name: '', module_type: 'standard_module', description: '' })
      refetch()
    } finally {
      setCreating(false)
    }
  }

  const handleDelete = async (name) => {
    if (!confirm(`'${name}' silinecek. Emin misiniz?`)) return
    await fetch(`${API}/modules/${name}`, { method: 'DELETE' })
    refetch()
  }

  if (loading) return <div className="loading">Yükleniyor...</div>

  return (
    <>
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3>🆕 Yeni Modül Oluştur</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
          <div className="form-group">
            <label>Modül Adı</label>
            <input
              value={form.name}
              onChange={e => setForm({ ...form, name: e.target.value })}
              placeholder="siparis_takip"
            />
          </div>
          <div className="form-group">
            <label>Tip</label>
            <select value={form.module_type} onChange={e => setForm({ ...form, module_type: e.target.value })}>
              <option value="analytics_module">Veri Analizi</option>
              <option value="api_service">API Servisi</option>
              <option value="worker_agent">Worker Agent</option>
              <option value="cli_tool">CLI Aracı</option>
              <option value="standard_module">Standart</option>
            </select>
          </div>
        </div>
        <div className="form-group">
          <label>Açıklama</label>
          <textarea
            value={form.description}
            onChange={e => setForm({ ...form, description: e.target.value })}
            placeholder="Ne yapmasını istiyorsunuz?"
          />
        </div>
        <button className="btn primary" onClick={handleCreate} disabled={creating}>
          {creating ? '⏳ Üretiliyor...' : '🚀 Modül Üret'}
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th>Modül</th>
            <th>Tip</th>
            <th>Versiyon</th>
            <th>Test</th>
            <th>Tarih</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {modules?.map(mod => (
            <tr key={mod.name}>
              <td><strong>{mod.name}</strong></td>
              <td><span className="badge info">{mod.type}</span></td>
              <td>{mod.version || '-'}</td>
              <td>{mod.has_tests ? '✅' : '❌'}</td>
              <td className="meta">{mod.registered_at?.slice(0, 10)}</td>
              <td>
                <button className="btn danger" style={{ padding: '0.3rem 0.8rem', fontSize: '0.8rem' }} onClick={() => handleDelete(mod.name)}>
                  Sil
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

// ─── Health ────────────────────────────────────────────────────
function Health() {
  const { data, loading } = useApi('/health')

  if (loading) return <div className="loading">Kontrol ediliyor...</div>

  const statusColor = data?.status === 'healthy' ? 'success' : data?.status === 'degraded' ? 'warning' : 'danger'

  return (
    <>
      <div className="stat-grid">
        <div className="stat-card">
          <div className="number" style={{ color: `var(--${statusColor})` }}>
            {data?.status?.toUpperCase()}
          </div>
          <div className="label">Sistem Durumu</div>
        </div>
        <div className="stat-card">
          <div className="number" style={{ color: 'var(--success)' }}>{data?.pass_count}</div>
          <div className="label">PASS</div>
        </div>
        <div className="stat-card">
          <div className="number" style={{ color: 'var(--warning)' }}>{data?.warn_count}</div>
          <div className="label">WARN</div>
        </div>
        <div className="stat-card">
          <div className="number" style={{ color: 'var(--danger)' }}>{data?.fail_count}</div>
          <div className="label">FAIL</div>
        </div>
      </div>

      <table>
        <thead>
          <tr><th>Bileşen</th><th>Durum</th><th>Detay</th></tr>
        </thead>
        <tbody>
          {data?.checks?.map((c, i) => (
            <tr key={i}>
              <td>{c.name}</td>
              <td>
                <span className={`badge ${c.status === 'PASS' ? 'success' : 'danger'}`}>
                  {c.status}
                </span>
              </td>
              <td className="meta">{c.output}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

// ─── Fleet ─────────────────────────────────────────────────────
function Fleet() {
  const { data, loading, refetch } = useApi('/fleet/devices')
  const { data: summary } = useApi('/fleet/summary')

  const registerSelf = async () => {
    await fetch(`${API}/fleet/register-self`, { method: 'POST' })
    refetch()
  }

  if (loading) return <div className="loading">Yükleniyor...</div>

  return (
    <>
      <div className="stat-grid">
        <div className="stat-card">
          <div className="number">{summary?.total_devices || 0}</div>
          <div className="label">Toplam Cihaz</div>
        </div>
        <div className="stat-card">
          <div className="number" style={{ color: 'var(--success)' }}>{summary?.healthy || 0}</div>
          <div className="label">Sağlıklı</div>
        </div>
        <div className="stat-card">
          <div className="number" style={{ color: 'var(--danger)' }}>{summary?.unhealthy || 0}</div>
          <div className="label">Sorunlu</div>
        </div>
        <div className="stat-card">
          <div className="number">{summary?.unique_modules || 0}</div>
          <div className="label">Benzersiz Modül</div>
        </div>
      </div>

      <button className="btn primary" onClick={registerSelf} style={{ marginBottom: '1rem' }}>
        📡 Bu Cihazı Kaydet
      </button>

      <table>
        <thead>
          <tr><th>Cihaz</th><th>Platform</th><th>Durum</th><th>Modüller</th><th>Son Heartbeat</th></tr>
        </thead>
        <tbody>
          {data?.map((d, i) => (
            <tr key={i}>
              <td><strong>{d.hostname || d.device_id}</strong></td>
              <td>{d.platform}</td>
              <td>
                <span className={`badge ${d.status === 'healthy' ? 'success' : d.status === 'degraded' ? 'warning' : 'danger'}`}>
                  {d.status}
                </span>
              </td>
              <td>{d.modules?.length || 0}</td>
              <td className="meta">{d.last_heartbeat?.slice(0, 19)}</td>
            </tr>
          ))}
          {(!data || data.length === 0) && (
            <tr><td colSpan={5} className="meta" style={{ textAlign: 'center' }}>Henüz kayıtlı cihaz yok</td></tr>
          )}
        </tbody>
      </table>
    </>
  )
}

// ─── App ───────────────────────────────────────────────────────
const TABS = [
  { id: 'dashboard', label: '📊 Dashboard', component: Dashboard },
  { id: 'modules', label: '📦 Modüller', component: Modules },
  { id: 'health', label: '🩺 Sağlık', component: Health },
  { id: 'fleet', label: '🌐 Filo', component: Fleet },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const ActiveComponent = TABS.find(t => t.id === activeTab)?.component || Dashboard

  return (
    <div className="app">
      <div className="header">
        <h1>🏭 Emare Hub Dashboard</h1>
        <p>Yazılım Fabrikası Yönetim Paneli</p>
      </div>

      <div className="tabs">
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <ActiveComponent />
    </div>
  )
}
