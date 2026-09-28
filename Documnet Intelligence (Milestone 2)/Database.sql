CREATE DATABASE `visondesk_ai`;
use `visondesk_ai`;
CREATE TABLE document_chunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    document_type VARCHAR(100),
    page_number INT,
    chunk_id VARCHAR(100),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO document_chunks
(filename, document_type, page_number, chunk_id, content)
VALUES
(
    'safety_manual.pdf',
    'Safety Manual',
    1,
    'chunk_1',
    'Workers must follow all safety procedures before operating machinery.'
),
(
    'safety_manual.pdf',
    'Safety Manual',
    2,
    'chunk_2',
    'Workers must wear helmets, gloves, safety shoes and protective goggles.'
),
(
    'safety_manual.pdf',
    'Safety Manual',
    3,
    'chunk_3',
    'Machines must be inspected before operation.'
);

SELECT * FROM document_chunks;

Alter table document_chunks add column file_type varchar(50);

SELECT * FROM document_chunks;

