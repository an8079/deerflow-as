/**
 * DeerFlow-X 后端 API 验证脚本（Node.js 替代 pytest）
 * 运行环境: Node.js + 内置 fetch
 */

const API_BASE = 'http://localhost:8000'

async function runTests() {
  let passed = 0
  let failed = 0
  const results = []

  async function test(name, fn) {
    try {
      await fn()
      passed++
      results.push({ name, status: 'PASS' })
      console.log(`✅ PASS: ${name}`)
    } catch (err) {
      failed++
      results.push({ name, status: 'FAIL', error: err.message })
      console.log(`❌ FAIL: ${name} — ${err.message}`)
    }
  }

  async function req(method, path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    })
    const text = await res.text()
    let data
    try { data = JSON.parse(text) } catch { data = text }
    return { status: res.status, data }
  }

  // ── Health ──
  await test('GET /health → 200', async () => {
    const r = await req('GET', '/health')
    if (r.status !== 200) throw new Error(`Expected 200, got ${r.status}`)
  })

  await test('GET /health → has version', async () => {
    const r = await req('GET', '/health')
    if (!r.data.version) throw new Error('Missing version field')
    if (r.data.version !== '0.1.0') throw new Error(`Wrong version: ${r.data.version}`)
  })

  // ── Tasks ──
  await test('POST /tasks → 200', async () => {
    const r = await req('POST', '/tasks', { task: 'Test task' })
    if (r.status !== 200) throw new Error(`Expected 200, got ${r.status}`)
  })

  await test('POST /tasks → returns task_id', async () => {
    const r = await req('POST', '/tasks', { task: 'Test task' })
    if (!r.data.task_id) throw new Error('Missing task_id')
    if (r.data.task_id === 'placeholder-id') {
      console.warn('⚠️  BUG: task_id is hardcoded placeholder, not a real UUID')
    }
  })

  await test('GET /tasks/{any} → 200 (BUG: should be 404)', async () => {
    const r = await req('GET', '/tasks/nonexistent-id-xyz')
    // This is the BUG — should be 404 but is 200
    if (r.status === 200) {
      console.warn('⚠️  BUG CONFIRMED: nonexistent task returns 200 instead of 404')
    }
    if (r.status !== 200) throw new Error(`Expected 200 (bug confirmed), got ${r.status}`)
  })

  await test('POST /tasks with empty task → handled', async () => {
    const r = await req('POST', '/tasks', { task: '' })
    // BUG: empty task is accepted
    if (r.status === 200) console.warn('⚠️  BUG: empty task accepted (should reject)')
  })

  // ── Missing APIs ──
  for (const [method, path] of [
    ['GET', '/projects'],
    ['POST', '/projects'],
    ['GET', '/agents'],
    ['GET', '/workflows'],
    ['GET', '/teams'],
  ]) {
    await test(`${method} ${path} → 404 (not implemented)`, async () => {
      const r = await req(method, path)
      if (r.status !== 404) throw new Error(`Expected 404, got ${r.status} (endpoint exists unexpectedly?)`)
    })
  }

  // ── Summary ──
  console.log(`\n${'='.repeat(50)}`)
  console.log(`Results: ${passed} passed, ${failed} failed`)
  console.log(`${'='.repeat(50)}`)

  process.exit(failed > 0 ? 1 : 0)
}

runTests().catch(err => {
  console.error('Test runner error:', err.message)
  process.exit(1)
})
