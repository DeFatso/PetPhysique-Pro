import React, { useState } from 'react';

const PetPhysiqueProForm: React.FC = () => {
  const [formData, setFormData] = useState({
    weight: '',
    age: '',
    height: '',
    breed: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/api/calculate_physique_pro', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result);
        // Handle the result (update state, display result, etc.)
      } else {
        console.error('Failed to fetch');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Weight:
        <input type="text" name="weight" value={formData.weight} onChange={handleChange} />
      </label>
      {/* Repeat for other input fields */}

      <button type="submit">Calculate Physique Pro</button>
    </form>
  );
};

export default PetPhysiqueProForm;
