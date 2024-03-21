import React from 'react';
import { Button, Card, Badge } from '@nextui-org/react';

interface ProductProps {
    name: string;
    description: string;
    url: string;
}

const Product: React.FC<ProductProps> = ({ name, description, url }) => {
    return (
        <Card className='p-8 w-1/3 gap-3'>
            <h3 className='text-xl font-bold'>{name}</h3>
            <p>{description}</p>
            <Button onClick={() => {window.location.href=`${url}`}}>开始使用</Button>
        </Card>
    );
};

export default Product;