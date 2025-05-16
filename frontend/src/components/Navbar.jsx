import { Link } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useState } from "react";

export default function Navbar({ onDateChange, selectedDate }) {
  const [error, setError] = useState(null);
  const [localDate, setLocalDate] = useState(null);

  const isOldDate = (date) => {
    const twoWeeksAgo = new Date();
    twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);
    return date < twoWeeksAgo;
  };

  const renderDayContents = (day, date) => {
    const shouldBlur = isOldDate(date);
    return (
      <div className={shouldBlur ? "opacity-50 blur-[1px]" : ""}>
        {day}
      </div>
    );
  };

  const handleDateChange = (date) => {
    try {
      setLocalDate(date);
      const event = {
        target: {
          value: date ? formatDateForInput(date) : ''
        }
      };
      onDateChange(event);
    } catch (err) {
      setError(err.message);
      console.error('Error handling date change:', err);
    }
  };

  const handleResetToToday = () => {
    setLocalDate(null);
    const event = {
      target: {
        value: ''
      }
    };
    onDateChange(event);
  };

  const formatDateForInput = (date) => {
    if (!date) return '';
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  return (
    <div >
    <nav className="flex flex-col sm:flex-row justify-between items-center w-full mx-auto max-w-3xl px-4 py-4 gap-4 sm:gap-0 bg-[rgb(214,198,173)]">
      <div>
        <Link to="/" onClick={handleResetToToday}>
          <h1 className="text-3xl sm:text-4xl font-quadrillion text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-violet-500">
            BuzzBrief
          </h1>
        </Link>
      </div>

      <div className="flex flex-col sm:flex-row items-center gap-3 sm:gap-4 w-full sm:w-auto">
        {error && (
          <div className="text-red-500 text-sm text-center">
            {error}
          </div>
        )}
        
        <div className="relative w-full sm:w-auto">
          <div className="absolute inset-0 z-0 rounded-lg"></div>
          <DatePicker
            selected={localDate}
            onChange={handleDateChange}
            dateFormat="yyyy-MM-dd"
            className="relative z-10 w-full sm:w-auto border border-gray-300 rounded-lg px-4 py-2 focus:outline-none cursor-pointer bg-[#e4d3bf] placeholder:text-gray-500"
            maxDate={new Date()}
            placeholderText="Select a date"

            isClearable
            renderDayContents={renderDayContents}
            filterDate={date => !isOldDate(date)}
            
          />
        </div>
      </div>
    </nav>
    </div>
  );
}
