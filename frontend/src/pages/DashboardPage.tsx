import { useEffect } from 'react';
import { useAuth } from '../context/useAuth';
import { useEstimates } from '../hooks/useEstimates';
import './DashboardPage.css';

const DashboardPage = () => {
  const { logout } = useAuth();
  const { estimates, loading, error, fetchEstimates, createEstimate } = useEstimates();

  useEffect(() => {
    if (!estimates) {
      fetchEstimates();
    }
  }, [fetchEstimates, estimates]);

  const handleLogout = () => {
    logout();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    createEstimate({
      customer_name: e.target[0].value,
      vehicle_model: e.target[1].value,
      vehicle_year: e.target[2].value,
      vehicle_mileage: e.target[3].value,
      repair_description: e.target[4].value,
      estimated_cost: e.target[5].value,
    });
  };

  if (loading) {
    return <p>Loading estimates...</p>;
  }

  if (error) {
    return <p>Error fetching estimates: {error}</p>;
  }

  return (
    <div className='dashboard-container'>
      <div className="dashboard-header">
        <h1>Repair Estimates</h1>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
      <div className="estimates-list">
        {estimates.map((estimate) => (
          <div key={estimate.id} className="estimate-item">
            <p>Customer Name: <span>{estimate.customer_name}</span></p>
            <p>Vehicle Model: <span>{estimate.vehicle_model}</span></p>
            <p>Vehicle Year: <span>{estimate.vehicle_year}</span></p>
            <p>Vehicle Mileage: <span>{estimate.vehicle_mileage}</span></p>
            <p>Repair Description: <span>{estimate.repair_description}</span></p>
            <p>Estimated Cost: <span>{estimate.estimated_cost}</span></p>
            <p>Status: <span>{estimate.status}</span></p>
          </div>
        ))}
      </div>
      <div className='create-estimate'>
        <h2>Create New Estimate</h2>
        <form className="create-estimate-form" onSubmit={handleSubmit}>
          <div className="input-container">
            <label>Customer Name:</label>
            <input type="text" placeholder="Enter customer name" />
          </div>
          <div className="input-container">
            <label>Vehicle Model:</label>
            <input type="text" placeholder="Enter vehicle model" />
          </div>
          <div className="input-container">
            <label>Vehicle Year:</label>
            <input type="number" placeholder="Enter vehicle year" />
          </div>
          <div className="input-container">
            <label>Vehicle Mileage:</label>
            <input type="number" placeholder="Enter vehicle mileage" />
          </div>
          <div className="input-container">
            <label>Repair Description:</label>
            <textarea placeholder="Enter repair description" rows={4}></textarea>
          </div>
          <div className="input-container">
            <label>Estimated Cost:</label>
            <input type="number" placeholder="Enter estimated cost" />
          </div>
          <button type="submit">Create Estimate</button>
        </form>
      </div>
    </div>
  );
}

export default DashboardPage;