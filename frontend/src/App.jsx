import { useState, useEffect } from 'react'
import './index.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

function App() {
  const [activeTab, setActiveTab] = useState('users')
  const [users, setUsers] = useState([])
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  // Form states
  const [userForm, setUserForm] = useState({ name: '', email: '' })
  const [productForm, setProductForm] = useState({ name: '', price: '', description: '' })
  const [orderForm, setOrderForm] = useState({ user_id: '', product_id: '', quantity: '' })

  useEffect(() => {
    fetchUsers()
    fetchProducts()
    fetchOrders()
  }, [])

  const showMessage = (type, message) => {
    if (type === 'error') {
      setError(message)
      setSuccess(null)
    } else {
      setSuccess(message)
      setError(null)
    }
    setTimeout(() => {
      setError(null)
      setSuccess(null)
    }, 5000)
  }

  // Users
  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/users`)
      if (!response.ok) throw new Error('Failed to fetch users')
      const data = await response.json()
      setUsers(data)
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  const createUser = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userForm)
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to create user')
      }
      showMessage('success', 'User created successfully')
      setUserForm({ name: '', email: '' })
      fetchUsers()
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  const deleteUser = async (id) => {
    if (!confirm('Are you sure you want to delete this user?')) return
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Failed to delete user')
      showMessage('success', 'User deleted successfully')
      fetchUsers()
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  // Products
  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/products`)
      if (!response.ok) throw new Error('Failed to fetch products')
      const data = await response.json()
      setProducts(data)
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  const createProduct = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: productForm.name,
          price: parseFloat(productForm.price),
          description: productForm.description
        })
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to create product')
      }
      showMessage('success', 'Product created successfully')
      setProductForm({ name: '', price: '', description: '' })
      fetchProducts()
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  const deleteProduct = async (id) => {
    if (!confirm('Are you sure you want to delete this product?')) return
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/products/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) throw new Error('Failed to delete product')
      showMessage('success', 'Product deleted successfully')
      fetchProducts()
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  // Orders
  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/orders`)
      if (!response.ok) throw new Error('Failed to fetch orders')
      const data = await response.json()
      setOrders(data)
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  const createOrder = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: parseInt(orderForm.user_id),
          product_id: parseInt(orderForm.product_id),
          quantity: parseInt(orderForm.quantity)
        })
      })
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to create order')
      }
      showMessage('success', 'Order created successfully')
      setOrderForm({ user_id: '', product_id: '', quantity: '' })
      fetchOrders()
    } catch (err) {
      showMessage('error', err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Microservices Application</h1>
        <p>User, Product, and Order Management</p>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          Users
        </button>
        <button
          className={`tab ${activeTab === 'products' ? 'active' : ''}`}
          onClick={() => setActiveTab('products')}
        >
          Products
        </button>
        <button
          className={`tab ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          Orders
        </button>
      </div>

      {activeTab === 'users' && (
        <div className="section">
          <h2>Create User</h2>
          <form onSubmit={createUser}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={userForm.name}
                onChange={(e) => setUserForm({ ...userForm, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={userForm.email}
                onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="button success" disabled={loading}>
              Create User
            </button>
          </form>

          <div className="list">
            <h2>Users List</h2>
            {loading ? (
              <div className="loading">Loading...</div>
            ) : users.length === 0 ? (
              <p>No users found</p>
            ) : (
              users.map((user) => (
                <div key={user.id} className="list-item">
                  <h3>{user.name}</h3>
                  <p>Email: {user.email}</p>
                  <p>ID: {user.id}</p>
                  <button
                    className="button danger"
                    onClick={() => deleteUser(user.id)}
                    disabled={loading}
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'products' && (
        <div className="section">
          <h2>Create Product</h2>
          <form onSubmit={createProduct}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={productForm.name}
                onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Price</label>
              <input
                type="number"
                step="0.01"
                value={productForm.price}
                onChange={(e) => setProductForm({ ...productForm, price: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={productForm.description}
                onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
              />
            </div>
            <button type="submit" className="button success" disabled={loading}>
              Create Product
            </button>
          </form>

          <div className="list">
            <h2>Products List</h2>
            {loading ? (
              <div className="loading">Loading...</div>
            ) : products.length === 0 ? (
              <p>No products found</p>
            ) : (
              products.map((product) => (
                <div key={product.id} className="list-item">
                  <h3>{product.name}</h3>
                  <p>Price: ${product.price}</p>
                  <p>Description: {product.description || 'N/A'}</p>
                  <p>ID: {product.id}</p>
                  <button
                    className="button danger"
                    onClick={() => deleteProduct(product.id)}
                    disabled={loading}
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'orders' && (
        <div className="section">
          <h2>Create Order</h2>
          <form onSubmit={createOrder}>
            <div className="form-group">
              <label>User ID</label>
              <input
                type="number"
                value={orderForm.user_id}
                onChange={(e) => setOrderForm({ ...orderForm, user_id: e.target.value })}
                required
                placeholder="Enter user ID"
              />
            </div>
            <div className="form-group">
              <label>Product ID</label>
              <input
                type="number"
                value={orderForm.product_id}
                onChange={(e) => setOrderForm({ ...orderForm, product_id: e.target.value })}
                required
                placeholder="Enter product ID"
              />
            </div>
            <div className="form-group">
              <label>Quantity</label>
              <input
                type="number"
                value={orderForm.quantity}
                onChange={(e) => setOrderForm({ ...orderForm, quantity: e.target.value })}
                required
                min="1"
              />
            </div>
            <button type="submit" className="button success" disabled={loading}>
              Create Order
            </button>
          </form>

          <div className="list">
            <h2>Orders List</h2>
            {loading ? (
              <div className="loading">Loading...</div>
            ) : orders.length === 0 ? (
              <p>No orders found</p>
            ) : (
              orders.map((order) => (
                <div key={order.id} className="list-item">
                  <h3>Order #{order.id}</h3>
                  <p>User ID: {order.user_id}</p>
                  <p>Product ID: {order.product_id}</p>
                  <p>Quantity: {order.quantity}</p>
                  <p>Total Price: ${order.total_price}</p>
                  <p>Created: {new Date(order.created_at).toLocaleString()}</p>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App

