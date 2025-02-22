import React from 'react';

const FormattedResult = ({ result }) => {
  // If result is a string, try to parse it into an object.
  let data = result;
  if (typeof result === 'string') {
    try {
      data = JSON.parse(result);
    } catch (err) {
      // If parsing fails, show the raw string.
      return <p className="text-gray-200 whitespace-pre-wrap">{result}</p>;
    }
  }

  return (
    <div className="space-y-6">
      {/* Google Fact Check API */}
      {data["Google Fact Check API"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Google Fact Check API</h3>
          <ul className="list-disc list-inside text-gray-200">
            {data["Google Fact Check API"].map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Wikipedia */}
      {data["Wikipedia"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Wikipedia</h3>
          <p className="text-gray-200">{data["Wikipedia"]}</p>
        </div>
      )}

      {/* Online Search */}
      {data["Online Search"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Online Search</h3>
          <div className="space-y-4">
            {data["Online Search"].map((entry, idx) => (
              <div key={idx} className="p-4 bg-gray-600 rounded-md">
                <p className="text-blue-400 font-semibold">{entry[0]}</p>
                <a
                  href={entry[1]}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-200 hover:underline"
                >
                  {entry[1]}
                </a>
                <p className="text-gray-200">{entry[2]}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Style Analysis */}
      {data["Style Analysis"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Style Analysis</h3>
          <p className="text-gray-200">
            Reading Ease Score: {data["Style Analysis"]["Reading Ease Score"]}
          </p>
          <p className="text-gray-200">
            Difficult Words Count: {data["Style Analysis"]["Difficult Words Count"]}
          </p>
        </div>
      )}

      {/* Source Credibility */}
      {data["Source Credibility"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Source Credibility</h3>
          <ul className="list-disc list-inside text-gray-200">
            {Object.entries(data["Source Credibility"]).map(([url, credibility]) => (
              <li key={url}>
                <a
                  href={url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-200 hover:underline"
                >
                  {url}
                </a>
                : {credibility}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Final Judgment (Local LLM) */}
      {data["Final Judgment (Local LLM)"] && (
        <div>
          <h3 className="text-xl font-semibold text-green-400">Final Judgment (Local LLM)</h3>
          <p className="whitespace-pre-wrap text-gray-200">{data["Final Judgment (Local LLM)"]}</p>
        </div>
      )}
    </div>
  );
};

export default FormattedResult;
