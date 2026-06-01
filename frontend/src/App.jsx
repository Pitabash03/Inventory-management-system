import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [products, setProducts] = useState([]);

  const [name, setName] = useState("");
  const [sku, setSku] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");

  const [customerName, setCustomerName] = useState("");
  const [customerEmail, setCustomerEmail] = useState("");

  // GET PRODUCTS
  const getProducts = async () => {
    const response = await axios.get("https://inventory-management-system-m8vl.onrender.com");
    setProducts(response.data);
  };

  useEffect(() => {
    getProducts();
  }, []);

  // ADD PRODUCT
  const addProduct = async () => {
    await axios.post("https://inventory-management-system-m8vl.onrender.com", {
      name,
      sku,
      price: Number(price),
      stock: Number(stock),
    });

    setName("");
    setSku("");
    setPrice("");
    setStock("");

    getProducts();
  };

  // ADD CUSTOMER
  const addCustomer = async () => {
    await axios.post("https://inventory-management-system-m8vl.onrender.com", {
      name: customerName,
      email: customerEmail,
    });

    alert("Customer Added");

    setCustomerName("");
    setCustomerEmail("");
  };

  // DELETE PRODUCT
  const deleteProduct = async (id) => {
    await axios.delete(`https://inventory-management-system-m8vl.onrender.com/${id}`);
    getProducts();
  };

  return (
    <div className="container">

      <h1>Inventory Management System</h1>

      {/* TOP SECTION */}
      <div className="top-section">

        {/* PRODUCT */}
        <div className="box">
          <h2>Add Product</h2>

          <input
            type="text"
            placeholder="Product Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            type="text"
            placeholder="SKU"
            value={sku}
            onChange={(e) => setSku(e.target.value)}
          />

          <input
            type="number"
            placeholder="Price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />

          <input
            type="number"
            placeholder="Stock"
            value={stock}
            onChange={(e) => setStock(e.target.value)}
          />

          <button onClick={addProduct}>
            Add Product
          </button>
        </div>

        {/* CUSTOMER */}
        <div className="box">
          <h2>Add Customer</h2>

          <input
            type="text"
            placeholder="Customer Name"
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
          />

          <input
            type="email"
            placeholder="Customer Email"
            value={customerEmail}
            onChange={(e) => setCustomerEmail(e.target.value)}
          />

          <button onClick={addCustomer}>
            Add Customer
          </button>
        </div>

      </div>

      {/* PRODUCTS */}
      <h2 className="product-title">Products List</h2>

      <div className="product-grid">

        {products.map((product) => (
          <div className="product-card" key={product.id}>

            <h3>{product.name}</h3>

            <p>Price: ₹{product.price}</p>
            <p>Stock: {product.stock}</p>
            <p>SKU: {product.sku}</p>

            <button onClick={() => deleteProduct(product.id)}>
              Delete
            </button>

          </div>
        ))}

      </div>

    </div>
  );
}

export default App;